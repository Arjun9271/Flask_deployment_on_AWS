from flask import Flask, render_template, request, jsonify
from dataclasses import dataclass
from typing import List, Optional
import re

app = Flask(__name__)

@dataclass
class PatternMatch:
    text: str
    start: int
    end: int
    group: str

@dataclass
class MatchResult:
    is_valid: bool
    matches: List[PatternMatch]
    message: str
    total_matches: int

    def to_dict(self):
        return {
            'is_valid': self.is_valid,
            'matches': [{'text': m.text, 'start': m.start, 'end': m.end, 'group': m.group} 
                       for m in self.matches],
            'message': self.message,
            'total_matches': self.total_matches
        }

class PatternMatcher:
    @staticmethod
    def find_matches(text: str, pattern: str) -> MatchResult:
        if not text or not pattern:
            return MatchResult(False, [], "Please provide both text and pattern", 0)

        try:
            regex = re.compile(pattern)
            matches = []

            for match in regex.finditer(text):
                matches.append(PatternMatch(
                    text=match.group(),
                    start=match.start(),
                    end=match.end(),
                    group=match.group()
                ))

            return MatchResult(
                is_valid=True,
                matches=matches,
                message=f"Success! Found {len(matches)} matches",
                total_matches=len(matches)
            )
        except re.error as e:
            return MatchResult(False, [], f"Invalid regex pattern: {str(e)}", 0)

class EmailValidator:
    EMAILPATTERN = r'^[a-zA-Z0-9.%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    @classmethod
    def validate_email(cls, email: str) -> MatchResult:
        if not email:
            return MatchResult(False, [], "Please provide an email address", 0)

        match = re.match(cls.EMAILPATTERN, email)  # Corrected from EMAIL_PATTERN to EMAILPATTERN
        if match:
            return MatchResult(True, [], "Valid email address format! ✓", 1)
        return MatchResult(False, [], "Invalid email address format ✗", 0)


@app.route("/")
def main_page():
    return render_template('regex_matcher.html', title="Pattern Matcher & Email Validator")

@app.route("/match_pattern", methods=['POST'])
def match_pattern():
    input_text = request.form.get('inputText', '')
    pattern = request.form.get('pattern', '')

    result = PatternMatcher.find_matches(input_text, pattern)
    return jsonify(result.to_dict())

@app.route("/validate_email", methods=['POST'])
def validate_email():
    email = request.form.get('email', '')
    result = EmailValidator.validate_email(email)
    return jsonify(result.to_dict())

if __name__ == "__main__":
    app.run(debug=True,host = "0.0.0.0")