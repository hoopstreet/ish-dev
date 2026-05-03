#!/bin/sh
. core/spinner.sh
. core/memory.sh
. core/executor.sh

init_memory

clear
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧠 HOOPSTREET AI AGENT v6.0 - PROFESSIONAL MODE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎯 I UNDERSTAND NATURAL LANGUAGE AND EXECUTE ACTIONS"
echo "💬 Just describe what you want me to do"
echo "📋 Examples:"
echo "   • 'Fix bugs and sync to GitHub'"
echo "   • 'Show system status'"
echo "   • 'Analyze GitHub repository'"
echo "   • 'Create a backup script'"
echo "   • 'Heal all errors'"
echo ""
echo "💡 Type 'menu' to exit"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

while true; do
    printf "\n💬 You: "
    read -r USER_INPUT
    [ "$USER_INPUT" = "menu" ] && break
    [ -z "$USER_INPUT" ] && continue
    
    echo ""
    run_with_spinner "Analyzing intent" sh core/planner.sh "$USER_INPUT" > /tmp/plan.json
    
    ACTION=$(jq -r '.action // "chat"' /tmp/plan.json)
    COMMAND=$(jq -r '.command // ""' /tmp/plan.json)
    CODE=$(jq -r '.code // ""' /tmp/plan.json)
    RESPONSE=$(jq -r '.response // "Processing..."' /tmp/plan.json)
    REMEMBER=$(jq -r '.remember // ""' /tmp/plan.json)
    
    echo "🤖 $RESPONSE"
    
    if [ "$ACTION" != "chat" ] && [ "$ACTION" != "null" ]; then
        echo ""
        run_with_spinner "Executing $ACTION" sh core/executor.sh "$ACTION" "$COMMAND" "$CODE" > /tmp/result.log
        cat /tmp/result.log | head -20
    fi
    
    [ -n "$REMEMBER" ] && save_knowledge "$REMEMBER" "learned"
    save_conversation "$USER_INPUT" "$RESPONSE"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
done
