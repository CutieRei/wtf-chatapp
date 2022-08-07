
export interface Message {
    sender: string
    content: string
}

export interface Messages extends Array<Message>{}

export interface SendMessage {
    (message: Message): void
}
