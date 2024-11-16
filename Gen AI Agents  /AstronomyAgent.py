import os
import openai
import tkinter as tk
from tkinter import scrolledtext, END
from openai import OpenAI
import sys
print(sys.executable)

# Set your OpenAI API key securely
client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
    )
print(os.environ.get("OPENAI_API_KEY"))
class AstronomyAgent:
    def __init__(self, system_prompt=""):
        self.system_prompt = system_prompt
        self.conversation = []
        if self.system_prompt:
            self.conversation.append({"role": "system", "content": self.system_prompt})

    def __call__(self, user_input):
        # Thought
        thought = f"The user asked: '{user_input}'. I need to provide a simple and clear explanation suitable for a child learning astronomy."
        self.conversation.append({"role": "assistant", "content": f"Thought: {thought}"})

        # Action
        action = "Consult knowledge base for an appropriate answer."
        self.conversation.append({"role": "assistant", "content": f"Action: {action}"})

        # Pause
        pause = "Waiting for information retrieval..."
        self.conversation.append({"role": "assistant", "content": f"Pause: {pause}"})

        # Observation
        observation = self.retrieve_information(user_input)
        self.conversation.append({"role": "assistant", "content": f"Observation: {observation}"})

        # Generate final answer
        final_answer = self.generate_answer()
        self.conversation.append({"role": "assistant", "content": final_answer})

        return final_answer

    def retrieve_information(self, query):
        # Simulate information retrieval
        print("....... in retrieve.......")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
            {"role": "system", "content": "Provide simple explanations suitable for a child."},
            {"role": "user", "content": query}
             ],
            max_tokens=150,
            temperature=0.5,
            n=1,
            stop=None,
        )
        return response.choices[0].message.content.strip()
    
    

    def generate_answer(self):
        # Exclude internal messages from the user's view
        messages_to_send = [msg for msg in self.conversation if not msg['content'].startswith(('Thought:', 'Action:', 'Pause:', 'Observation:'))]
        try:
            completion = client.chat.completions.create(
                messages=messages_to_send,
                temperature=0.5,
                model="gpt-4o"
                )
            return completion.choices[0].message.content.strip()
        except openai.error.OpenAIError as e:
            print(f"An error occurred: {e}")
            return "I'm sorry, but I couldn't process your request."
    
# Create the UI using Tkinter
class AstronomyTutorApp:
    def __init__(self, root, agent):
        self.root = root
        self.agent = agent
        self.root.title("Astronomy Tutor for Kids")

        # Create chat display area
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', width=120, height=40, font=("Helvetica", 12))
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Create input field
        self.user_input = tk.Entry(self.root, width=50, font=("Helvetica", 12))
        self.user_input.grid(row=1, column=0, padx=10, pady=(0, 10))

        # Create send button
        self.send_button = tk.Button(self.root, text="Ask", command=self.send_message, font=("Helvetica", 12))
        self.send_button.grid(row=1, column=1, padx=10, pady=(0, 10))

        # Bind enter key to send message
        self.root.bind('<Return>', lambda event: self.send_message())

        # Welcome message
        self.display_message("Agent", "Hello! I'm your Astronomy Tutor. Ask me anything about space!")

    def display_message(self, sender, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(END, f"{sender}: {message}\n\n")
        self.chat_display.yview(END)
        self.chat_display.config(state='disabled')

    def send_message(self):
        user_text = self.user_input.get()
        if user_text.strip() == "":
            return
        self.display_message("You", user_text)
        self.user_input.delete(0, END)

        # Get agent's response
        try:
            response = self.agent(user_text)
            self.display_message("Agent", response)
        except Exception as e:
            print(f"An error occurred: {e}")
            self.display_message("Agent", "Oops! Something went wrong. Please try again later.")

# Main function to run the app
def main():
    system_prompt = "You are an astronomy tutor helping a child learn about space. Use simple language and make the explanations engaging."
    agent = AstronomyAgent(system_prompt=system_prompt)

    root = tk.Tk()
    app = AstronomyTutorApp(root, agent)
    root.mainloop()

if __name__ == "__main__":
    main()