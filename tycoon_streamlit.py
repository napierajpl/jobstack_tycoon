import random
import streamlit as st
import pandas as pd

class Customer:
    def __init__(self):
        self.workers_needed = random.randint(1, 50)
        self.days_needed = random.randint(1, 14)
        self.min_budget = random.randint(10, 15)
        self.max_budget = random.randint(16, 25)  # Ensure max is always higher than min
        self.displayed_budget = random.randint(self.min_budget, self.max_budget)  # Hidden real budget range

    def accept_offer(self, bill_rate):
        return self.min_budget <= bill_rate <= self.max_budget


class Worker:
    def __init__(self):
        self.min_pay = random.randint(8, 14)
        self.max_pay = random.randint(self.min_pay, 50)  # Max pay is unlimited, just simulated
    
    def accept_offer(self, pay_rate):
        return pay_rate >= self.min_pay


class Game:
    def __init__(self):
        self.score = 0
        self.round_summaries = []  # To store summaries for each round
    
    def generate_customer(self):
        return Customer()
    
    def generate_workers(self, num_workers):
        return [Worker() for _ in range(num_workers)]
    
    def play_round(self, customer, workers, bill_rate, pay_rate):
        # Check if customer accepts the bill rate
        if not customer.accept_offer(bill_rate):
            return "Customer rejected the offer.", 0
        
        # Check if workers accept the pay rate
        accepted_workers = [worker for worker in workers if worker.accept_offer(pay_rate)]
        
        if len(accepted_workers) == 0:
            return f"No workers accepted the offer.", 0
        
        # Calculate the score
        hours_worked = len(accepted_workers) * customer.days_needed * 8  # 8 hours per day
        earnings = round((bill_rate - pay_rate) * hours_worked, 2)
        self.score += earnings

        # Maximum possible earnings (if using max_budget)
        max_earnings = round((customer.max_budget - pay_rate) * hours_worked, 2)

        # Calculate the percentage of potential earnings used
        if max_earnings > 0:
            percentage_earned = round((earnings / max_earnings) * 100, 2)
        else:
            percentage_earned = 0

        # Save the round details for the summary
        round_summary = {
            "Round": len(self.round_summaries) + 1,
            "Max Bill Rate": f"${customer.max_budget:.2f}",
            "Used Bill Rate": f"${bill_rate:.2f}",
            "Workers Needed": customer.workers_needed,
            "Workers Worked": len(accepted_workers),
            "Max Earnings": f"${max_earnings:.2f}",
            "Actual Earnings": f"${earnings:.2f}",
            "% of Potential Earned": f"{percentage_earned:.2f}%"
        }
        self.round_summaries.append(round_summary)
        
        return f"Round completed with {len(accepted_workers)} workers. Earnings: ${earnings:.2f}", earnings
    
    def game_summary(self):
        # Convert the summary data to a pandas DataFrame for easier display
        summary_df = pd.DataFrame(self.round_summaries)
        
        # Add a row for total values
        total_max_earnings = sum(float(row["Max Earnings"].replace('$', '')) for row in self.round_summaries)
        total_actual_earnings = sum(float(row["Actual Earnings"].replace('$', '')) for row in self.round_summaries)

        total_percentage_earned = round((total_actual_earnings / total_max_earnings) * 100, 2) if total_max_earnings > 0 else 0

        total_row = {
            "Round": "Total",
            "Max Bill Rate": "",
            "Used Bill Rate": "",
            "Workers Needed": sum(row["Workers Needed"] for row in self.round_summaries),
            "Workers Worked": sum(row["Workers Worked"] for row in self.round_summaries),
            "Max Earnings": f"${total_max_earnings:.2f}",
            "Actual Earnings": f"${total_actual_earnings:.2f}",
            "% of Potential Earned": f"{total_percentage_earned:.2f}%"
        }
        
        # Use pandas.concat instead of append
        summary_df = pd.concat([summary_df, pd.DataFrame([total_row])], ignore_index=True)

        return summary_df

# Initialize the game and the customer/worker for each round
def main():
    if "game" not in st.session_state:
        st.session_state.game = Game()
        st.session_state.round = 1
        st.session_state.round_completed = False  # Track if the current round is completed
        st.session_state.result_message = None  # Store round result message
    
    st.title("Jobstack Tycoon")

    # Game in progress
    if st.session_state.round <= 5:
        if not st.session_state.round_completed:
            st.header(f"Round {st.session_state.round}")

            # Generate a new customer and workers if it's a new round
            if "customer" not in st.session_state or st.session_state.customer is None:
                st.session_state.customer = st.session_state.game.generate_customer()
            
            customer = st.session_state.customer
            st.write(f"Customer needs {customer.workers_needed} workers for {customer.days_needed} days.")
            st.write(f"They say that you can bill them: ${round(customer.displayed_budget, 2):.2f} per hour (but you can offer something else).")

            # Player proposes bill rate
            bill_rate = st.slider("Propose a Bill Rate (per hour)", min_value=10.0, max_value=30.0, value=15.0)
            
            if "workers" not in st.session_state or st.session_state.workers is None:
                st.session_state.workers = st.session_state.game.generate_workers(customer.workers_needed)
            
            # Player proposes pay rate for workers
            pay_rate = st.slider("Propose a Pay Rate for Workers (per hour)", min_value=8.0, max_value=30.0, value=10.0)

            if st.button("Submit Offer"):
                # Play round and calculate score
                result_message, earnings = st.session_state.game.play_round(customer, st.session_state.workers, bill_rate, pay_rate)
                st.success(result_message)
                st.session_state.result_message = result_message
                st.session_state.round_completed = True  # Mark the round as completed
        else:
            # Display round result and OK button to move to the next round
            st.success(st.session_state.result_message)
            st.write(f"Your total score so far is: ${st.session_state.game.score:.2f}")
            if st.button("OK"):
                # Move to the next round and reset for the next round
                st.session_state.round += 1
                st.session_state.customer = None  # Reset customer for next round
                st.session_state.workers = None   # Reset workers for next round
                st.session_state.round_completed = False  # Reset the round status

    # Game over
    else:
        st.header("Game Over")
        st.write(f"Final Score: ${st.session_state.game.score:.2f}")
        # Generate and display the game summary
        summary_df = st.session_state.game.game_summary()
        st.write("Game Summary:")
        st.dataframe(summary_df, use_container_width=True)  # Use full width of the container to display the table
        
        if st.button("Restart Game"):
            st.session_state.clear()  # Reset the game state to start fresh

if __name__ == "__main__":
    st.set_page_config(page_title="Jobstack Tycoon", layout="centered")
    main()