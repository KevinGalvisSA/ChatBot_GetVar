# KAI Agent

chatbot_project/
│
├── app/
│   ├── adapters/
│   │   ├── http/
│   │   │   └── routes.py 
│   │── application/
│   │   └── chatbot.py 
│   ├── config/
│   │   └── bot_regulations.py
│   ├── domain/
│   │   ├── model/
│   │   │   └── user.py  
│   ├── infrastructure/
│   │   ├── qdrant.py  
│   │   ├── document_indexer.py 
│   │   ├── gemini_integration.py
│   │   ├── extract_info.py 
│   │   ├── langraph_orchestrator.py 
│   ├── models/
│   │   └── context_chunck.py   
│   ├── main.py 
│   ├── requirements.txt  
│   ├── .env 
├── config.py  
├── .gitignore
├── README_md
└── text_gemini.py  #Testeo del funcionamiento gemini
