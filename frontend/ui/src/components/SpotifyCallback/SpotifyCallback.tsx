import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';

const SpotifyCallback = () => {
    const navigate = useNavigate();
    const [error, setError] = useState('');

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');
        const error = urlParams.get('error');
        console.log(code);

        if (error) {
            setError('Spotify authentication failed');
            return;
        }

        if (code) {
            fetch('http://127.0.0.1:8000/api/exchange-code/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code }),
                credentials: 'include',
            })
            .then(response => response.json())
            .then(async data => {
                if (data.message === 'Successfully logged in') {
                    console.log("YES");
                    localStorage.setItem('username', data.username);
                    navigate('/');
                } else {
                    setError('Failed to log in with Spotify');
                }
            })
            .catch(err => {
                console.error('Error:', err);
                setError('Something went wrong');
            });
        }
    }, [navigate]);

    if (error) {
        return <div>{error}</div>;
    }

    return <div>Loading...</div>;
};

export default SpotifyCallback;
