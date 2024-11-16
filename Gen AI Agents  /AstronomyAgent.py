import os
import openai
import tkinter as tk
from tkinter import scrolledtext, END
from openai import OpenAI
import sys
print(sys.executable)

# Set your OpenAI API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        
        response = client.chat.completions.create(
            engine="text-davinci-003",
            prompt=f"Provide a simple explanation suitable for a child: {query}",
            max_tokens=150,
            temperature=0.5,
            n=1,
            stop=None,
        )
        return response.choices[0].text.strip()

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
    )

    def generate_answer(self):
        # Exclude internal messages from the user's view
        messages_to_send = [msg for msg in self.conversation if not msg['content'].startswith(('Thought:', 'Action:', 'Pause:', 'Observation:'))]
        completion = client.chat.completions.create(
                chat_completion = client.chat.completions.create(
                messages=messages_to_send,
                temperature=0.5,
                model="gpt-4o"
                )
            )
        return completion.choices[0].message.content.strip()

# Create the UI using Tkinter
class AstronomyTutorApp:
    def __init__(self, root, agent):
        self.root = root
        self.agent = agent
        self.root.title("Astronomy Tutor")

        # Create chat display area
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', width=60, height=20, font=("Helvetica", 12))
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
        response = self.agent(user_text)
        self.display_message("Agent", response)

# Main function to run the app
def main():
    # Set up the agent with a system prompt
    system_prompt = "You are an astronomy tutor helping a child learn about space. Use simple language and make the explanations engaging."
    agent = AstronomyAgent(system_prompt=system_prompt)

    # Create the main window
    root = tk.Tk()
    app = AstronomyTutorApp(root, agent)
    root.mainloop()

if __name__ == "__main__":
    main()