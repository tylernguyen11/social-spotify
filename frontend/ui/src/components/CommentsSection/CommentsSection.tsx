import React, { useState, useEffect } from 'react';
import {
    Textarea,
    Button,
    Group,
    Avatar,
    Text,
    Box,
    Divider,
    ScrollArea,
    Paper,
    Stack,
} from "@mantine/core";
import classes from './CommentsSection.module.css';

interface Comment {
    id: number;
    artist_id: string;
    username: string;
    content: string;
    created_at: string;
}

interface Props {
    artistId: string | undefined;
}

const CommentsSection: React.FC<Props> = ({ artistId }) => {
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
    const [loading, setLoading] = useState(true);
    const [comments, setComments] = useState<Comment[]>([]);
    const [newComment, setNewComment] = useState('');

    useEffect(() => {
        const fetchComments = async () => {
            const response = await fetch(`${API_BASE_URL}/api/comments/?artist_id=${artistId}`, { credentials: 'include' });
            const data = await response.json();
            setComments(data);
        };

        setLoading(false);
        fetchComments();
    }, [artistId]);

    const handleCommentSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/api/comments/`, {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ artist_id: artistId, content: newComment }),
            });
            if (response.ok) {
                const newCommentData = await response.json();
                setComments((prev) => [newCommentData, ...prev]);
                setNewComment('');
            }
        } catch (error) {
            console.error('Error posting comment:', error);
        } finally {
            setLoading(false);
        }
    };
    return (
        <div style={{ display: 'flex', flexDirection: 'column', width: '50vw' }}>
            <Text size="lg" mb="xs">
                Comments
            </Text>
            <ScrollArea style={{ height: 300 }} offsetScrollbars>
                {comments.map((comment) => (
                    <Paper withBorder p="md" radius="md" mb="sm" key={comment.id} bg='white'>
                        <Stack align='start'>
                            <Group>
                                <Avatar color="blue">{comment.username}</Avatar>
                                <Box>
                                    <Text c='black'>{comment.username}</Text>
                                    <Text size="xs" c="dimmed">
                                        {new Date(comment.created_at).toLocaleString()}
                                    </Text>
                                </Box>
                            </Group>
                            <Text pl={54} mt="sm" c='black'>{comment.content}</Text>
                        </Stack>
                    </Paper>
                ))}
            </ScrollArea>
            <Divider my="sm" />
            <Textarea
                placeholder="Write a comment..."
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                autosize
                minRows={2}
                maxRows={5}
                mb="sm"
                classNames={{ input: classes.input }}
            />
            <Group>
                <Button onClick={handleCommentSubmit} loading={loading}>
                    Post Comment
                </Button>
            </Group>
        </div>
    );
};



export default CommentsSection;