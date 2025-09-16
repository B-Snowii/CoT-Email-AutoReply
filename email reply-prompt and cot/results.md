model: DS\_API\_R1



\###############Prompt only###############

**++++large both---> top\_k=50, top\_p=0.9, temp=0.5**

reply: 25%, response: 0, action: 25%

Note: reply-yes to all, action: not include to all

**++++large k \&small p---> top\_k=50, top\_p=0.1, temp=0.3**

reply: 25%, response: 0, action: 25%

nothing changed?? Same response with large both

**++++large p \&small k---> top\_k=1, top\_p=0.9, temp=0.3**

**reply: 50%**, response: 0, action: 50%

++++small both**---> top\_k=1, top\_p=0.1, temp=0.3**

reply: 25%, response: 0, action: 50%

**++++large p \&median k---> top\_k=25, top\_p=0.9, temp=0.3**

*MVP*reply: 50%, response: 25%, action: 50%

**++++large p \&median k 2---> top\_k=35, top\_p=0.8, temp=0.5**

reply: 25%, response: 0, action: 50%

**++++large p \&median k 3---> top\_k=15, top\_p=0.8, temp=0.5**

**++++median p \&median k--->top\_k=25, top\_p=0.5, temp=0.3**

reply: 25%, response: 0, action: 50%

**++++large p only---> top\_k=1, top\_p=0.9, temp=0.3**

reply: 25%, response: 0, action: 50%



\###############CoT-Deepseek###############

**++++large p \&median k---> top\_k=25, top\_p=0.9, temp=0.3**

100% at all!

**++++small p \&large k---> top\_k=50, top\_p=0.1, temp=0.3**

100% at all!

**++++small both---> top\_k=1, top\_p=0.1, temp=0.3**

100% at all!

**++++large both---> top\_k=50, top\_p=0.9, temp=0.7**

100% at all!

\###############CoT-Llama2###############
**++++unchange parameters**
reply: 75%, response: 50%, action: 75%
**++++MVP option---> top\_k=25, top\_p=0.9, temp=0.3**
**differenct position-->different result?**
*temp p k*: reply: 75%, response: 50%, action: 100%*MVP*
*temp k  p*: 0,  25%, 75%
*k p temp*: 0, 25%, 100%
*p temp k*:25%, 50%, 100%
*k temp p*:50%, 25%, 100%


Message	

Sounds good, thank you Researcher!			

Thanks for reaching out. No I would like to opt out of the series for this paper. Thanks.			

Hi Researcher, that would be great, thank you!			

"Happy for the chapter to be included in your series. Please note that it is in the process of also being included in the Academic Partner working paper

&nbsp;series, so I am not sure how you will go about the cover page (since Academic Partner also likes to add theirs)."			

++++Researcher

Reply No, No, No, Yes

Response NA, NA, NA, We typically skip the cover page for Academic Partner-covered papers because we understand how much the Academic Partner recognition means to researchers. 

Action include, not include, include, include



