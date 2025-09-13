import tkinter as tk
from tkinter import ttk, messagebox
import re
import string

class PasswordStrengthChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Checker")
        self.root.geometry("550x600")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Password Strength Checker",
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=(0, 14))
        
        # Password input frame
        input_frame = tk.Frame(main_frame, bg='#f0f0f0')
        input_frame.pack(fill='x', pady=(0, 16))
        
        # Password label
        password_label = tk.Label(
            input_frame,
            text="Enter Password:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        )
        password_label.pack(anchor='w', pady=(0, 5))
        
        # Password entry with show/hide functionality
        entry_frame = tk.Frame(input_frame, bg='#f0f0f0')
        entry_frame.pack(fill='x')
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            entry_frame,
            textvariable=self.password_var,
            font=('Arial', 10),
            show='*',
            width=40
        )
        self.password_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.password_entry.bind('<KeyRelease>', self.on_password_change)
        
        # Show/Hide password button
        self.show_password = tk.BooleanVar()
        self.toggle_btn = tk.Checkbutton(
            entry_frame,
            text="Show",
            variable=self.show_password,
            command=self.toggle_password_visibility,
            bg='#f0f0f0',
            font=('Arial', 10)
        )
        self.toggle_btn.pack(side='right')
        
        # Strength indicator frame
        strength_frame = tk.Frame(main_frame, bg='#f0f0f0')
        strength_frame.pack(fill='x', pady=(0, 16))
        
        # Strength label
        strength_label = tk.Label(
            strength_frame,
            text="Password Strength:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        )
        strength_label.pack(anchor='w', pady=(0, 5))
        
        # Progress bar
        self.progress = ttk.Progressbar(
            strength_frame,
            length=400,
            mode='determinate',
            style='Strength.Horizontal.TProgressbar'
        )
        self.progress.pack(fill='x', pady=(0, 10))
        
        # Strength text and score
        score_frame = tk.Frame(strength_frame, bg='#f0f0f0')
        score_frame.pack(fill='x')
        
        self.strength_label = tk.Label(
            score_frame,
            text="Very Weak",
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0',
            fg='#ff4444'
        )
        self.strength_label.pack(side='left')
        
        self.score_label = tk.Label(
            score_frame,
            text="Score: 0/10",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#666666'
        )
        self.score_label.pack(side='right')
        
        # Criteria frame
        criteria_frame = tk.LabelFrame(
            main_frame,
            text="Password Criteria",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            fg='#333333',
            padx=10,
            pady=10
        )
        criteria_frame.pack(fill='x', pady=(0, 16))
        
        # Criteria checkmarks
        self.criteria_labels = {}
        criteria = [
            ("length", "At least 8 characters long"),
            ("lowercase", "Contains lowercase letters (a-z)"),
            ("uppercase", "Contains uppercase letters (A-Z)"),
            ("digits", "Contains numbers (0-9)"),
            ("special", "Contains special characters (!@#$%^&*)"),
            ("patterns", "Avoids common patterns")
        ]
        
        for key, text in criteria:
            frame = tk.Frame(criteria_frame, bg='#f0f0f0')
            frame.pack(fill='x', pady=2)
            
            icon = tk.Label(
                frame,
                text="❌",
                font=('Arial', 10),
                bg='#f0f0f0'
            )
            icon.pack(side='left', padx=(0, 10))
            
            label = tk.Label(
                frame,
                text=text,
                font=('Arial', 10),
                bg='#f0f0f0',
                fg='#666666',
                anchor='w'
            )
            label.pack(side='left', fill='x', expand=True)
            
            self.criteria_labels[key] = {'icon': icon, 'label': label}
        
        # Suggestions frame
        suggestions_frame = tk.LabelFrame(
            main_frame,
            text="Suggestions for Improvement",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            fg='#333333',
            padx=15,
            pady=15
        )
        suggestions_frame.pack(fill='both', expand=True)
        
        # Suggestions text widget with scrollbar
        text_frame = tk.Frame(suggestions_frame, bg='#f0f0f0')
        text_frame.pack(fill='both', expand=True)
        
        self.suggestions_text = tk.Text(
            text_frame,
            height=8,
            wrap=tk.WORD,
            font=('Arial', 10),
            bg='white',
            fg='#333333',
            padx=10,
            pady=10,
            state='disabled'
        )
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.suggestions_text.yview)
        self.suggestions_text.configure(yscrollcommand=scrollbar.set)
        
        self.suggestions_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Generate password button
        generate_btn = tk.Button(
            main_frame,
            text="Generate Strong Password",
            font=('Arial', 10, 'bold'),
            bg='#4CAF50',
            fg='white',
            command=self.generate_password,
            cursor='hand2',
            padx=20,
            pady=10
        )
        generate_btn.pack(pady=(15, 0))
        
        # Initial check with empty password
        self.check_password("")
    
    def toggle_password_visibility(self):
        if self.show_password.get():
            self.password_entry.configure(show='')
        else:
            self.password_entry.configure(show='*')
    
    def on_password_change(self, event=None):
        password = self.password_var.get()
        self.check_password(password)
    
    def check_password_strength(self, password):
        """Check password strength and return results."""
        score = 0
        feedback = []
        criteria_met = {
            'length': False,
            'lowercase': False,
            'uppercase': False,
            'digits': False,
            'special': False,
            'patterns': True
        }
        
        # Check length
        if len(password) >= 12:
            score += 3
            criteria_met['length'] = True
        elif len(password) >= 8:
            score += 2
            criteria_met['length'] = True
        elif len(password) >= 6:
            score += 1
        else:
            feedback.append("• Use at least 8 characters (12+ recommended)")
        
        # Check for lowercase letters
        if re.search(r'[a-z]', password):
            score += 1
            criteria_met['lowercase'] = True
        else:
            feedback.append("• Add lowercase letters (a-z)")
        
        # Check for uppercase letters
        if re.search(r'[A-Z]', password):
            score += 1
            criteria_met['uppercase'] = True
        else:
            feedback.append("• Add uppercase letters (A-Z)")
        
        # Check for digits
        if re.search(r'\d', password):
            score += 1
            criteria_met['digits'] = True
        else:
            feedback.append("• Add numbers (0-9)")
        
        # Check for special characters
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
            criteria_met['special'] = True
        else:
            feedback.append("• Add special characters (!@#$%^&*(),.?\":{}|<>)")
        
        # Check for variety in character types
        char_types = sum([
            any(c.islower() for c in password),
            any(c.isupper() for c in password),
            any(c.isdigit() for c in password),
            any(c in string.punctuation for c in password)
        ])
        
        if char_types >= 4:
            score += 2
        elif char_types >= 3:
            score += 1
        
        # Check for common patterns
        common_patterns = [
            r'123456', r'abcdef', r'qwerty', r'password', r'admin',
            r'(.)\1{2,}',  # repeated characters
            r'(012|123|234|345|456|567|678|789|890)',  # sequential numbers
            r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)'
        ]
        
        pattern_found = False
        for pattern in common_patterns:
            if re.search(pattern, password.lower()):
                pattern_found = True
                break
        
        if pattern_found:
            feedback.append("• Avoid common patterns like '123456', 'qwerty', or repeated characters")
            criteria_met['patterns'] = False
            score -= 1
        else:
            score += 1
        
        # Determine strength level
        if score >= 9:
            strength = "Very Strong"
            color = "#4CAF50"  # Green
        elif score >= 7:
            strength = "Strong"
            color = "#8BC34A"  # Light Green
        elif score >= 5:
            strength = "Moderate"
            color = "#FF9800"  # Orange
        elif score >= 3:
            strength = "Weak"
            color = "#FF5722"  # Red Orange
        else:
            strength = "Very Weak"
            color = "#F44336"  # Red
        
        return {
            'score': max(0, score),
            'max_score': 10,
            'strength': strength,
            'color': color,
            'feedback': feedback,
            'criteria_met': criteria_met
        }
    
    def check_password(self, password):
        """Update UI based on password strength."""
        result = self.check_password_strength(password)
        
        # Update progress bar
        progress_value = (result['score'] / result['max_score']) * 100
        self.progress['value'] = progress_value
        
        # Configure progress bar color
        self.style.configure(
            'Strength.Horizontal.TProgressbar',
            troughcolor='#e0e0e0',
            background=result['color']
        )
        
        # Update strength label
        self.strength_label.configure(
            text=result['strength'],
            fg=result['color']
        )
        
        # Update score label
        self.score_label.configure(
            text=f"Score: {result['score']}/{result['max_score']}"
        )
        
        # Update criteria checkmarks
        for key, met in result['criteria_met'].items():
            icon = self.criteria_labels[key]['icon']
            label = self.criteria_labels[key]['label']
            
            if met:
                icon.configure(text="✅", fg="#4CAF50")
                label.configure(fg="#4CAF50")
            else:
                icon.configure(text="❌", fg="#F44336")
                label.configure(fg="#666666")
        
        # Update suggestions
        self.suggestions_text.configure(state='normal')
        self.suggestions_text.delete(1.0, tk.END)
        
        if result['feedback']:
            suggestions = "\n".join(result['feedback'])
            self.suggestions_text.insert(tk.END, suggestions)
        else:
            self.suggestions_text.insert(tk.END, "🎉 Excellent! Your password meets all security criteria.")
        
        self.suggestions_text.configure(state='disabled')
    
    def generate_password(self):
        """Generate a strong password."""
        import random
        
        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*(),.?\":{}|<>"
        
        # Ensure at least one character from each category
        password_chars = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special)
        ]
        
        # Fill remaining length with random characters
        all_chars = lowercase + uppercase + digits + special
        for _ in range(8):  # Total length will be 12
            password_chars.append(random.choice(all_chars))
        
        # Shuffle the password
        random.shuffle(password_chars)
        generated_password = ''.join(password_chars)
        
        # Set the generated password
        self.password_var.set(generated_password)
        self.check_password(generated_password)
        
        # Show message
        messagebox.showinfo(
            "Password Generated",
            f"A strong password has been generated:\n\n{generated_password}\n\nIt has been entered in the password field."
        )

def main():
    root = tk.Tk()
    app = PasswordStrengthChecker(root)
    root.mainloop()

if __name__ == "__main__":
    main()