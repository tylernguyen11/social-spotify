import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import { ArtistProps } from '../../interfaces/app_interfaces';
import CommentsSection from '../CommentsSection/CommentsSection';
import { Title, Text, Badge} from "@mantine/core";
import '@mantine/core/styles.css';
import '@mantine/carousel/styles.css';
import ImageCarousel from '../ImageCarousel/ImageCarousel';
import { SpotifyProps } from '../../interfaces/app_interfaces';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const ArtistPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [artist, setArtist] = useState<ArtistProps | null>(null);
    const [albums, setAlbums] = useState<SpotifyProps[]>([]);
    const [topTracks, setTopTracks] = useState<SpotifyProps[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchArtistDetails = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/artists/${id}/`, {
                    credentials: 'include',
                });
                if (!response.ok) {
                    throw new Error('Failed to fetch artist details');
                }
                const data = await response.json();
                setArtist(data.artist);
                setAlbums(data.albums);
                setTopTracks(data.top_tracks);
            } catch (err: any) {
                setError(err.message || 'An error occurred');
            } finally {
                setLoading(false);
            }
        };

        fetchArtistDetails();
    }, [id]);

    if (loading) return <p>Loading artist details...</p>;
    if (error) return <p style={{ color: 'red' }}>{error}</p>;

    return (
        <div style={{ textAlign: 'center', margin: 0, width: '100vw', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            {artist && (
                <>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '1rem', justifyContent: 'center' }}>
                        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                            {artist.image_url && (
                                <a href={artist.spotify_url} target="_blank" rel="noopener noreferrer">
                                    <img src={artist.image_url} alt={artist.name} style={{ width: '12vw', height: '12vw', borderRadius: '50%' }} />
                                </a>
                            )}
                            <div>
                                {artist.genres.map((genre) => (
                                    <Badge>{genre}</Badge>
                                ))}
                            </div>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'start', justifyContent: 'center' }}>
                            <Text size="xs">Artist</Text>
                            <Title size="4rem">{artist.name}</Title>
                            <Text>Followers: {artist.followers.toLocaleString()}</Text>
                        </div>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'center' }}>
                        <ImageCarousel items={albums}></ImageCarousel>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'center' }}>
                        <ImageCarousel items={topTracks}></ImageCarousel>
                    </div>
                </>
            )}
            <h1>Comments</h1>
            <CommentsSection artistId={id}></CommentsSection>
        </div>
    );
};

export default ArtistPage;
