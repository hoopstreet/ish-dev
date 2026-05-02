
@bot.on(events.NewMessage())
async def flow(event):
    # If the user sends a new command, cancel any pending state
    if event.text.startswith('/'):
        if event.sender_id in user_state:
            del user_state[event.sender_id]
        return 

    if event.sender_id not in user_state: return
    state = user_state[event.sender_id]
    
    if state['step'] == 'sched':
        try:
            # Clean the input
            clean_date = event.text.strip()
            datetime.strptime(clean_date, '%Y-%m-%d %H:%M')
            database.set_setting('schedule_time', clean_date)
            await event.respond(f"📅 Set for: {clean_date}")
            del user_state[event.sender_id]
        except: 
            await event.respond("❌ Format: YYYY-MM-DD HH:MM\n(Example: 2026-04-29 08:00)")
