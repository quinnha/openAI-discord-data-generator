# openAI-discord-data-generator
JSONL generator for discord logs, which can be used to fine-tune OpenAI models.

## Background
With the release of OpenAI API, it's now possible (and easier than ever) to use their models in your application. One use is creating an AI bot of yourself, this repository gathers training data from discord logs and cleans them into a usable JSONL file for openAI CLI data preparation tool. 


OpenAI requires a JSONL file to finetune data, which looks something like this:
```json
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
```
This program uses the reply source as the `"prompt"`, and your reply message as the `"completion"`

Currently data is only cleaned by word length (excluding @s), further optimization can be done to better select quality message for training.


## Getting Started

### Prerequisites
* [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter)
* openai
  ```sh
  pip install openai
  ```

### Installation

1. Export as many discord text channels as you want with DiscordChatExporter as JSON files. 
2. Clone the repo
   ```sh
   git clone https://github.com/quinnha/openAI-discord-data-generator.git
   ```
3. Create a new folder called `/log`
   ```sh
   cd openAI-discord-data-generator
   mkdir log
   ```
4. Drop your JSON files from step 1 into `/log`
5. Edit USER_NAME and DISCRIMINATOR in `parse.py` to your discord tag. For example, if your discord tag is `quinnha#1234`, it should look like 
```py
USER_NAME = "quinnha"
DISCRIMINATOR = "1234"
```
6. Run `parse.py`
  ```py
   python parse.py
   ```
   Output should be similar
   ```
   Operation complete, find the log in output.jsonl
   
   Replies Parsed: 1440
   
   Words Parsed: 29896
   
   Approximate Tokens: 39861
   ```
   
6. Run OpenAI's CLI data preparation tool to confirm correctness
```sh
   openai tools fine_tunes.prepare_data -f output.jsonl
   ```

Lastly, follow openAI Finetuning API [documentation](https://platform.openai.com/docs/guides/fine-tuning) to create and use your model!

## To-Do
- [ ] Compare quality of completions of discord reply data to a hand-picked set of prompts and ansewrs
- [ ] Determine logic to better parse/clean data
- [ ] Create a GUI to use

