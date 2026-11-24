import os, base64
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from openai import AsyncOpenAI
from app.agents import AGENTS, get_agent

app=FastAPI(title="ORCA Founder Voice Team")
client=AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None
class AgentRequest(BaseModel):
 message:str=Field(min_length=1,max_length=5000)
 context:str=Field(default="ORCA companion. Live repository/deployment status is not connected unless verified.",max_length=12000)
async def generate_turn(agent_id,message,context):
 if client is None: raise HTTPException(503,"Configure OPENAI_API_KEY in the environment.")
 agent=get_agent(agent_id)
 try:
  c=await client.chat.completions.create(model=os.getenv("ORCA_CHAT_MODEL","gpt-4.1-mini"),messages=[{"role":"system","content":agent.prompt},{"role":"user","content":f"Project context:\n{context}\n\nTask:\n{message}"}],max_tokens=650,temperature=.35)
  text=c.choices[0].message.content or "No response yet."
  audio=await client.audio.speech.create(model=os.getenv("ORCA_TTS_MODEL","gpt-4o-mini-tts"),voice=agent.voice,input=text[:4000],instructions=agent.style+" Speak naturally. This is AI-generated speech.",response_format="mp3")
  return {"agent":agent.id,"name":agent.name,"role":agent.role,"text":text,"audio_base64":base64.b64encode(await audio.aread()).decode("ascii"),"ai_generated":True}
 except HTTPException: raise
 except Exception as e: raise HTTPException(502,"LLM or speech failed: "+type(e).__name__) from e
@app.get("/api/agents")
def agents(): return {"disclosure":"AI-generated speech","agents":[{"id":a.id,"name":a.name,"title":a.title,"role":a.role,"voice":a.voice} for a in AGENTS.values()]}
@app.post("/api/agent/{agent_id}/respond")
async def respond(agent_id:str,request:AgentRequest): return await generate_turn(agent_id,request.message,request.context)
@app.post("/api/standup")
async def standup(request:AgentRequest):
 agenda=[("miles","Open founder stand-up and state agenda."),("atlas","Developer update, next engineering step, blockers; do not invent repository status."),("astra","Product strategy, roadmap and one founder decision."),("nova","Research options, risks and uncertainties."),("miles","Close with decisions, owners, action items and acceptance criteria.")]
 turns=[]
 for aid,prompt in agenda: turns.append(await generate_turn(aid,prompt,request.context))
 return {"host":"Miles","turns":turns,"sequential":True,"ai_generated":True}
@app.get("/",response_class=HTMLResponse)
def home(): return Path(__file__).with_name("index.html").read_text(encoding="utf-8")
