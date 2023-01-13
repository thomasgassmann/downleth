export type Timeframe = {
    timezone: string;
    from: string;
    to: string;
}

export type ScheduleType = 'weekly' | 'once';

export type When = {
    schedule: ScheduleType;
    timeframe: Timeframe;
}

export type Stream = {
    when: When;
    where: string | string[];
    name: string;
    detail?: string;
}

export type Recording = {
    department: string;
    year: string;
    semester: 'autumn' | 'spring';
    number: string;
    name: string;
}

export type Config = {
    $schema: string;
    cache_location: string | null;
    streams: Stream[];
    recordings: Recording[];
}
