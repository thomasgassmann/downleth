export type Timeframe = {
    timezone: string;
    from: string;
    to: string;
}

export type When = {
    schedule: 'weekly' | 'once';
    timeframe: Timeframe;
}

export type Stream = {
    when: When;
    where: string | string[];
    name: string;
    detail?: string;
}

export type Config = {
    $schema: string;
    cache_location: string | null;
    streams: Stream[]
}
