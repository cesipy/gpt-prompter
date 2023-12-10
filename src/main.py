import os
from openai import OpenAI
import sys
import typing
import token_helper

# get openai api key
my_api_key = os.getenv('OPENAI_API_KEY')

# openai client
client = OpenAI(
    api_key=my_api_key
)

PATH = '../res/text.txt'              # modify here if needed

message_history = [
    {"role": "system", "content": "act like donald trump."}
    ]
follow_up_prompt = "ask 5 follow-up questions to the system's responses."

# ------------------------------------------------------------------ #

def parse_args() -> typing.Tuple[str, str]:
    """
    parses command line arguments. returns model and mode. 
    """
    help_message = """ 
        usage: python main.py <-flag>

        flags: 
        --gpt3 for gpt3.5-turbo
        --gpt4 for gpt4
        --gpt3-16k for gpt3.5-turbo-16k
        --gpt4-32k for gpt4-32k
        --follow-up for follow up questions (main.py <optional: gpt-model> --follow-up)
        """
    
    model = "gpt-3.5-turbo-1106"  # Default model
    mode = "default"

    if len(sys.argv) > 1: 
        if sys.argv[1] == "--gpt3-16k":
            model = "gpt-3.5-turbo-16k"

        elif sys.argv[1] == "--gpt3":
            model = "gpt-3.5-turbo-1106"

        elif sys.argv[1] == "--gpt4":
            model = "gpt-4"

        elif sys.argv[1] == "--gpt4-32k":
            model = "gpt-4-32k"

        elif sys.argv[1] == "--follow-up":
            mode = "follow-up"

        elif sys.argv[1] == "--token-count":
            mode = "token-count"
        
        elif sys.argv[1] in ["--help", "--usage"]:
            print(help_message)
            sys.exit(0)

        else:
            print(help_message)
            sys.exit(0)
        
    if len(sys.argv) == 3 and sys.argv[2] == "--follow-up":
        mode = "follow-up"

    return model, mode


def read_text_file(path: str) -> str:
    with open(path) as f:
        text = f.read()
    
    return text


def get_response( gpt_model: str) -> typing.Tuple[str, int]: 
    """
    generates an openai-api request and processes it. 
    returns the request result and token usage
    
    @param gpt_model - specifies language model, used in api request.

    @return api result, token_usage
    """
    completion  = client.chat.completions.create(
        model   =gpt_model, 
        messages=message_history
        )
    result: str = completion.choices[0].message.content
                                                    
    input_token :int       = completion.usage.prompt_tokens
    output_token:int       = completion.usage.completion_tokens
    token_usage:(int, int) = (input_token, output_token)

    return result, token_usage


def generate_follow_up(gpt_model) -> str:
    """
    generates follow-up questions and appends them  to message history
    """
    prompt: str = follow_up_prompt
    add_to_history("system", prompt)

    response: str = get_response(gpt_model)

    return response


def add_to_history(role: str, input_text: str) -> None:
    """
    adds the text to the message history
    
    @param role - can be `user` or `role`
    """
    if role != "user" and role != "system":
        raise Exception ("wrong user for history appending!")
        sys.exit()

    message = {"role": role, "content" : input_text}
    message_history.append(message)


def print_info(model, tokens) -> None:
    """
    prints information about the prompt(s). 
    information message includes the model used, 
    total amount of tokens and amount of prompt in cents.
    """
    fees: float  = calculate_price(model, tokens)
    total_tokens = tokens[0] + tokens[1]
    message = f"""
        using model: {model}
        tokens     : {total_tokens}
        fees       : {fees} cent

-

    """
    print(message)


def calculate_price(model: str, token_usage : typing.Tuple[int, int]) -> float:
    """
    calculates the total price of prompt collection in cents.

    @param model - gpt model, necessary for calculation.
    @param token_usage - a tupel (int, int) containing in- and output token
    usage (in 1ks)
    """
    input_token_1k  = token_usage[0] / 1000.0
    output_token_1k = token_usage[1] / 1000.0
    match model: 
        case "gpt-3.5-turbo-1106": 
            input_price = input_token_1k  * 0.1
            output_pice = output_token_1k * 0.2

        case "gpt-3.5-turbo": 
            input_price = input_token_1k  * 0.15                 # in cent
            output_pice = output_token_1k * 0.2                  

        case "gpt-4":
            input_price = input_token_1k  * 3                 # in cent
            output_pice = output_token_1k * 6                  

        case "gpt-3.5-turbo-16k":
            input_price = input_token_1k  * 0.3                 # in cent
            output_pice = output_token_1k * 0.4

        case _: 
            input_price = input_token_1k  * 0.0                # in cent
            output_pice = output_token_1k * 0.0

    return round(input_price + output_pice, 3)


def main():                
    model, mode    = parse_args()           # fetch model (gpt3.5-turbo, gpt4, ...) 
                                            # and mode (esp. follow-up mode)
    prompting_text = read_text_file(PATH)      
    add_to_history('user', prompting_text)

    if mode == "token-count":
        num_token = token_helper.token_counter(prompting_text, model)
        print(f"token count: {num_token}")
        return

    response       = get_response(model)    # response[0] is text, 
                                            # response[1] is token_usage
    add_to_history("system", response[0])
    print("\n", response[0], "\n\n-\n")
    tokens         = response[1]

    if mode == "follow-up":
        # get follow-up questions
        response: (str, int)      = generate_follow_up(model)
        follow_up_questions: str  = response[0]
        tokens += response[1]               # adjust token count
        
        add_to_history("user", follow_up_questions)

        # process follow-up questions
        response = get_response(model)
        answer   = response[0]
        tokens  += response[1]              # adjust token count

        add_to_history("system", response[0])
        
        print( follow_up_questions, "\n-\n\n", answer)

    print_info(model, tokens)               # add information about token usage


if __name__ == '__main__':
    main()
