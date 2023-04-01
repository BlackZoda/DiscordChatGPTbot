from tokenizers import Tokenizer, models, pre_tokenizers, decoders, processors

tokenizer = Tokenizer(models.BPE())
tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=True)
tokenizer.decoder = decoders.ByteLevel()
tokenizer.post_processor = processors.TemplateProcessing(
    single="$0", special_tokens=[("[CLS]", 0), ("[SEP]", 1)]
)

text = "This is a test message."
tokenized = tokenizer.encode(text)
print("Number of tokens:", len(tokenized.ids))
