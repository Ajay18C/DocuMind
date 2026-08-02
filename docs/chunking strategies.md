# Chunking Strategies

## Fixed size chunking + Top K retrieval:

This is essentialy splitting the document in a fixed length and then get the most similar part and giving to llm for the answer.

### Things to note:
1. If the size grows very big the question to a specific thing is harder to be similar with the part
2. If it is very small more parts matches with question if we took top k few might get missed as well
3. llm only have the knowledge within the parts
4. It will be usefull to find the similar portions but asking clarificaiton and finding answer for the question is difficult unless if the full context in the chunk
5. It will really helpful to see if there any related content in the document that's it. Just for identifying.


## Semantic chunking + Top K retrieval:

This is basically clubing the semantically similar chunks together inorder to keep the continuity

### Things to note:
1. It still only have the knowledge within the chunks and llm knowledge
2. 