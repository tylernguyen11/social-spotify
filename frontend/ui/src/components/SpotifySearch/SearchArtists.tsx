import React, { useState } from 'react';
import { ArtistProps } from '../../interfaces/app_interfaces';
import { Link } from 'react-router';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const SearchArtists: React.FC = () => {
    const [query, setQuery] = useState(''); // State for the search query
    const [artists, setArtists] = useState<ArtistProps[]>([]);
    const [loading, setLoading] = useState(false); // State for loading status
    const [error, setError] = useState<string | null>(null); // State for error messages

    const handleSearch = async () => {
        if (!query.trim()) return; // Don't search with an empty query

        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`${API_BASE_URL}/api/search?q=${query}`, {
                method: 'GET',
                credentials: 'include', // To include cookies for session-based auth
                headers: { 'Content-Type': 'application/json' },
            });

            if (!response.ok) {
                throw new Error('Failed to fetch artists');
            }

            const data = await response.json();
            setArtists(data.artists || []); // Update artists with the response data
        } catch (err: any) {
            setError(err.message || 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>Search Spotify Artists</h1>
            <div style={{ marginBottom: '1rem' }}>
                <input
                    type="text"
                    placeholder="Search for an artist"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    style={{
                        padding: '0.5rem',
                        marginRight: '0.5rem',
                        border: '1px solid #ccc',
                        borderRadius: '4px',
                    }}
                />
                <button
                    onClick={handleSearch}
                    style={{
                        padding: '0.5rem 1rem',
                        backgroundColor: '#1DB954',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                    }}
                >
                    Search
                </button>
            </div>
            {loading && <p>Loading...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
                {artists.map((artist) => (
                    <div
                        key={artist.id}
                        style={{
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            width: '150px',
                        }}
                    >
                        <Link to={`/artists/${artist.id}`}>
                        <img
                            src={artist.image_url || 'https://via.placeholder.com/150'}
                            alt={artist.name}
                            style={{
                                width: '100%',
                                height: '150px',
                                objectFit: 'cover',
                                borderRadius: '8px',
                            }}
                        />
                        </Link>
                        <p style={{ textAlign: 'center', marginTop: '0.5rem' }}>
                            {artist.name}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SearchArtists;
