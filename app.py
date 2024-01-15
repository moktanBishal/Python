from flask import Flask, render_template, request, make_response

app = Flask(__name__)

class FundraisingCampaign:
    def __init__(self, goal_amount):
        self.total_funds = 0
        self.goal_amount = goal_amount

    def get_valid_donation(self, donation_input):
        try:
            donation_amount = float(donation_input)
            if donation_amount > 0:
                return donation_amount
            else:
                return None
        except ValueError:
            return None

    def display_thank_you_message(self):
        return "Thank you for your donation!"

    def display_progress(self):
        progress_percentage = (self.total_funds / self.goal_amount) * 100
        return f"We have reached {progress_percentage:.2f}% of our goal."

    def reset_form_values(self):
        self.total_funds = 0

    def fund_progress(self):
        return f"Fund collected: ${self.total_funds} "

fundraising_campaign = FundraisingCampaign(goal_amount=10000)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        donation_input = request.form["donation"]
        donation_amount = fundraising_campaign.get_valid_donation(donation_input)

        if donation_amount is not None:
            fundraising_campaign.total_funds += donation_amount

        # Check if a specific condition is met (e.g., button click) to reset form values
        if 'reset_button' in request.form:
            fundraising_campaign.reset_form_values()

    return render_template("index.html",
                           thank_you_message=fundraising_campaign.display_thank_you_message(),
                           progress_message=fundraising_campaign.display_progress(),
                           fund_collected=fundraising_campaign.fund_progress())

if __name__ == "__main__":
    app.run(debug=True)
