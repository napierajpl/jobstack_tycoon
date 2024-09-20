import random

class Customer:
    def __init__(self):
        self.workers_needed = random.randint(1, 50)
        self.days_needed = random.randint(1, 14)
        self.min_budget = random.randint(10, 15)
        self.max_budget = random.randint(16, 25)  # Ensure max is always higher than min
    
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
        self.customers = []
        self.workers = []
        self.score = 0
    
    def generate_customer(self):
        customer = Customer()
        self.customers.append(customer)
        return customer
    
    def generate_workers(self, num_workers):
        self.workers = [Worker() for _ in range(num_workers)]
        return self.workers
    
    def play_round(self):
        # Generate customer
        customer = self.generate_customer()
        print(f"Customer needs {customer.workers_needed} workers for {customer.days_needed} days.")
        print(f"Customer's budget is between {customer.min_budget} and {customer.max_budget} per hour.")
        
        # Player proposes bill rate
        bill_rate = float(input("Propose a bill rate per hour: "))
        
        # Check if customer accepts the bill rate
        if not customer.accept_offer(bill_rate):
            print("Customer rejected the offer.")
            return 0
        
        # Generate workers and propose pay rate
        workers = self.generate_workers(customer.workers_needed)
        pay_rate = float(input("Propose a pay rate for workers: "))
        
        # Check if workers accept the pay rate
        accepted_workers = [worker for worker in workers if worker.accept_offer(pay_rate)]
        
        # If not enough workers accept, we proceed with available workers
        if len(accepted_workers) < customer.workers_needed:
            print(f"Not enough workers accepted the offer. Proceeding with {len(accepted_workers)} workers.")
        
        # Calculate hours worked and earnings
        hours_worked = len(accepted_workers) * customer.days_needed * 8  # 8 hours per day
        earnings = (bill_rate - pay_rate) * hours_worked
        self.score += earnings
        
        print(f"Round completed. You earned {earnings} this round.")
        print(f"Your total score after this round is: {self.score}")
        return earnings
    
    def calculate_score(self):
        print(f"Your final score after 5 rounds is: {self.score}")


# Example of running the game
def main():
    game = Game()
    
    for round_num in range(5):  # 5 rounds of the game
        print(f"\n--- Round {round_num + 1} ---")
        game.play_round()
    
    game.calculate_score()

if __name__ == "__main__":
    main()