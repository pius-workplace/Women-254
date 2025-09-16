# Women 254 Chatbot - Issues Fixed ✅

## 1. Missing Dependencies ✅
- [x] Add llama_index packages to requirements.txt
- [x] Add chromadb to requirements.txt
- [x] Add torch and transformers for HuggingFace embeddings

## 2. File Format Mismatch ✅
- [x] Update main.py to load CSV files instead of .txt/.pdf/.docx
- [x] Update test_chroma.py to use CSV loading
- [x] Update test_load.py to use CSV loading

## 3. API Key Consistency ✅
- [x] Standardize API key naming (use GEMINI_API_KEY consistently)
- [x] Update rag.py to use GEMINI_API_KEY instead of GOOGLE_API_KEY

## 4. Embedding Model Consistency
- [ ] Choose one embedding approach (recommend HuggingFace for local/offline)
- [ ] Update rag.py to use HuggingFace embeddings
- [ ] Remove OpenAI dependency if not needed

## 5. Application Reference Fix ✅
- [x] Update run.sh to reference main:app instead of app:app
- [ ] Create app.py if needed for proper module structure

## 6. Testing
- [ ] Test the application startup
- [ ] Test the query endpoint
- [ ] Verify CSV data loading works
