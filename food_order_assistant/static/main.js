let currentConversationId = null;

        document.getElementById('questionForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const question = document.getElementById('question').value;
            if (!question) return;

            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';

            try {
                const response = await fetch('/question', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ question }),
                });

                const data = await response.json();
                
                displayEnhancedAnswer(data.answer);
                document.getElementById('result').style.display = 'block';
                currentConversationId = data.conversation_id;
            } catch (error) {
                console.error('Error:', error);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });

        function displayEnhancedAnswer(answer) {
            const answerElement = document.getElementById('answer');
            answerElement.innerHTML = '';

            const lines = answer.split('\n');
            lines.forEach(line => {
                const div = document.createElement('div');
                
                // Highlight text between asterisks
                line = line.replace(/\*\*(.*?)\*\*/g, '<span class="bold-text">$1</span>');
                
                // Create new line for numbered items
                if (/^\d+\./.test(line)) {
                    div.className = 'menu-item';
                }
                
                div.innerHTML = line;
                answerElement.appendChild(div);
            });
        }

        async function provideFeedback(feedback) {
            if (!currentConversationId) return;

            try {
                const response = await fetch('/feedback', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        conversation_id: currentConversationId,
                        feedback: feedback
                    }),
                });

                const data = await response.json();
                alert(data.message);
            } catch (error) {
                console.error('Error:', error);
            }
        }