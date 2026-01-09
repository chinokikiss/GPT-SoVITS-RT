import re
import torch
from config import tts_config
from GPT_SoVITS.text.LangSegmenter import LangSegmenter
from GPT_SoVITS.text import cleaned_text_to_sequence
from GPT_SoVITS.text.cleaner import clean_text


def cut_text(text, punds, cut_minlen):
    text = text.strip("\n")
    mergeitems = []
    items = []

    for i, char in enumerate(text):
        if char in punds and len(items) > cut_minlen:
            if char == "." and i > 0 and i < len(text) - 1 and text[i - 1].isdigit() and text[i + 1].isdigit():
                items.append(char)
            else:
                items.append(char)
                mergeitems.append("".join(items))
                items = []
        else:
            items.append(char)

    if items:
        mergeitems.append("".join(items))

    return [item for item in mergeitems if not set(item).issubset(punds)]


def clean_text_inf(text, language):
    language = language.replace("all_", "")
    phones_raw, word2ph, norm_text = clean_text(text, language)
    phones = cleaned_text_to_sequence(phones_raw)
    return phones, word2ph, norm_text


def get_phones_and_bert(text, language):
    text = re.sub(r' {2,}', ' ', text)
    textlist = []
    langlist = []
    if language == "all_zh":
        for tmp in LangSegmenter.getTexts(text,"zh"):
            langlist.append(tmp["lang"])
            textlist.append(tmp["text"])
    elif language == "all_yue":
        for tmp in LangSegmenter.getTexts(text,"zh"):
            if tmp["lang"] == "zh":
                tmp["lang"] = "yue"
            langlist.append(tmp["lang"])
            textlist.append(tmp["text"])
    elif language == "all_ja":
        for tmp in LangSegmenter.getTexts(text,"ja"):
            langlist.append(tmp["lang"])
            textlist.append(tmp["text"])
    elif language == "all_ko":
        for tmp in LangSegmenter.getTexts(text,"ko"):
            langlist.append(tmp["lang"])
            textlist.append(tmp["text"])
    elif language == "en":
        langlist.append("en")
        textlist.append(text)
    elif language == "auto":
        for tmp in LangSegmenter.getTexts(text):
            langlist.append(tmp["lang"])
            textlist.append(tmp["text"])
    elif language == "auto_yue":
        for tmp in LangSegmenter.getTexts(text):
            if tmp["lang"] == "zh":
                tmp["lang"] = "yue"
            langlist.append(tmp["lang"])
            textlist.append(tmp["text"])
    else:
        for tmp in LangSegmenter.getTexts(text):
            if langlist:
                if (tmp["lang"] == "en" and langlist[-1] == "en") or (tmp["lang"] != "en" and langlist[-1] != "en"):
                    textlist[-1] += tmp["text"]
                    continue
            if tmp["lang"] == "en":
                langlist.append(tmp["lang"])
            else:
                langlist.append(language)
            textlist.append(tmp["text"])

    phones_list = []
    bert_list = []
    norm_text_list = []
    word2ph = {"word":[], "ph":[]}
    for i in range(len(textlist)):
        lang = langlist[i]
        phones, _word2ph, norm_text = clean_text_inf(textlist[i], lang)
        if _word2ph:
            word2ph["word"] += _word2ph["word"]
            word2ph["ph"] += _word2ph["ph"]
        if tts_config.cnroberta and "zh" in lang:
            bert = tts_config.cnroberta(norm_text, word2ph["ph"])
        else:
            bert = torch.zeros((1024, len(phones)), dtype=tts_config.dtype).to(tts_config.device)
        phones_list.append(phones)
        norm_text_list.append(norm_text)
        bert_list.append(bert)
    bert = torch.cat(bert_list, dim=1)
    phones = sum(phones_list, [])
    norm_text = "".join(norm_text_list)

    return phones, word2ph, bert, norm_text


def sub2text_index(subtitles, norm_text: str, orig_text: str):
    idx = 0
    sub_norm_idx = []
    for subtitle in subtitles:
        text = subtitle['text']
        idx = norm_text.find(text, idx)
        sub_norm_idx.append({"start":idx, "end":idx+len(text)-1})
    
    idx = 0
    norm_orig_idx = []
    for chr in norm_text:
        i = orig_text.find(chr, idx)
        if i != -1: idx = i
        norm_orig_idx.append(i)
    
    last_i = 0
    last_orig_idx = None
    for i, orig_idx in enumerate(norm_orig_idx+[len(orig_text)]):
        if orig_idx == -1 and last_orig_idx != -1:
            last_i = i
        elif orig_idx != -1 and last_orig_idx == -1:
            for j in range(last_i, i):
                norm_orig_idx[j] = int((j-last_i+1) * (orig_idx-1) / (i-last_i))
        last_orig_idx = orig_idx
    
    for i, norm_idx in enumerate(sub_norm_idx):
        orig_idx_start, orig_idx_end = norm_orig_idx[norm_idx["start"]], norm_orig_idx[norm_idx["end"]]
        subtitles[i]["orig_idx_start"] = orig_idx_start
        subtitles[i]["orig_idx_end"] = orig_idx_end + 1
    
    return subtitles