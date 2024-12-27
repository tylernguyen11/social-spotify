const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const LoginButton = () => {
    const handleLogin = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/login/`, {credentials: "include"});
            const data = await response.json();
            if (data.url) {
                window.location.href = data.url;
            } else {
                console.error('No URL returned from the backend');
            }
        } catch (error) {
            console.error('Error initiating Spotify login:', error);
        }
    };
    
    return (
        <button onClick={handleLogin} className="spotify-login-button">
        Login with Spotify
        </button>
    );
};

export default LoginButton;
