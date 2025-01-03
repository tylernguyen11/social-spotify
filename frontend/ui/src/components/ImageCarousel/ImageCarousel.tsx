import React from 'react';
import { Title, Image, HoverCard, Text } from '@mantine/core';
import { Carousel } from '@mantine/carousel';
import { SpotifyProps } from '../../interfaces/app_interfaces';

interface Props {
    items: SpotifyProps[];
}

const ImageCarousel: React.FC<Props> = ({items}) => {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'start' }}>
            <Title>Albums</Title>
            <Carousel
                withIndicators
                height={180}
                slideSize={60}
                slideGap='sm'
                loop
                align="start"
                includeGapInSize={true}
                slidesToScroll={4}
                w='1000'
            >
                {items.map((p) => (
                    <Carousel.Slide key={p.id}>
                        <HoverCard shadow="md">
                            <HoverCard.Target>
                                <a href={p.spotify_url} target="_blank" rel="noopener noreferrer">
                                    <Image src={p.image_url} alt={p.name} h={150} w={150} />
                                </a>
                            </HoverCard.Target>
                            <HoverCard.Dropdown>
                                <Text size="sm" color="black">
                                    {p.name}
                                </Text>
                            </HoverCard.Dropdown>
                        </HoverCard>
                    </Carousel.Slide>
                ))}
            </Carousel>
        </div>
    )
}

export default ImageCarousel;