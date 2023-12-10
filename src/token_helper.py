# tokenize helper 
# https://stackoverflow.com/questions/75804599/openai-api-how-do-i-count-tokens-before-i-send-an-api-request
import tiktoken


def encoding_getter(encoding_type: str):
    """
    returns the appropriate encoding based on the given encoding type (either an encoding string or a model name).
    
    @param encoding_type - model string (e.g. "gpt-3.5-turbo-16k")
    """
    if "k_base" in encoding_type:
        return tiktoken.get_encoding(encoding_type)
    else:
        return tiktoken.encoding_for_model(encoding_type)


def tokenizer(string: str, encoding_type: str) -> list:
    """
    returns the tokens in a text string using the specified encoding.

    @param string - input string to measure token length
    @param encoding_type - model string (e.g. "gpt-3.5-turbo-16k")
    """
    encoding = encoding_getter(encoding_type)
    tokens = encoding.encode(string)
    return tokens


def token_counter(string: str, encoding_type: str) -> int:
    """
    returns the number of tokens in a text string using the specified encoding.
    
    @param string - input string to measure token length
    @param encoding_type - model string (e.g. "gpt-3.5-turbo-16k")
    """
    num_tokens = len(tokenizer(string, encoding_type))
    return num_tokens

