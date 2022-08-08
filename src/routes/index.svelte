<script lang="ts">
	import { io } from "socket.io-client";
	// import Navbar from "../components/Navbar.svelte";
	import { afterUpdate, onMount } from "svelte";
	import type { Messages } from "$lib/messages"

	let authenticated = false;
	let name = "";
	let messages: Messages = []
	let previousLength: number = 0;
	let msg = "";
	let sendMsg = () => {};

	function scrollMessageBottom() {
		let div = document.querySelector("#messages")
		div?.scroll({top: div?.scrollHeight, behavior: "smooth"})
	}

	onMount(() => {
		scrollMessageBottom()
	})

	function resolveUri() {
		return window.location.origin.replace(`:${window.location.port}`, ":5174")
	}

	async function submit() {
		if(name.length == 0) return
		const sio = io(resolveUri(), {
			query: { name: name },
			path: "/gateaway/socket.io"
		});

		sio.on("messageAdd", (data) => {
			previousLength = messages.length
			messages = [...messages, data]
		});

		sio.on("connect", async () => {
			sendMsg = () => {
				if(msg.length == 0) {
					return
				};
				sio.emit("messageAdd", {msg:{content: msg}});
				msg = "";
			}
			authenticated = true;
			messages = await fetch(resolveUri()+"/messages").then(r => r.json());
		});
	};

	afterUpdate(() => {
		if(previousLength < messages.length) {
			scrollMessageBottom();
			previousLength = messages.length;
		}
	})
</script>

<main class="bg-neutral w-screen h-screen flex flex-col">
	{#if !authenticated}
		<div class="w-full h-full flex justify-center items-center">
			<form id="name-form" class="flex flex-col bg-primary p-10 rounded-xl" on:submit|preventDefault="{submit}">
				<input class="outline-none focus:outline-2 focus:outline-secondary" bind:value="{name}" placeholder="name">
				<button disabled="{name.length <= 1}" class="bg-neutral hover:bg-secondary enabled:hover:text-white disabled:bg-secondary">Submit</button>
			</form>
		</div>
	{:else}
		<div id="messages" class="w-full h-full overflow-y-scroll scrollbar scrollbar-thumb-slate-400">
			<ul class="list-none p-0 m-1">
				{#each messages as msg}
					<li class="pl-2 mb-5">
						<p style="{msg.sender === 'System' ? 'color: #3182ce' : ''}" class="text-xl font-semibold">{msg.sender}</p>
						<p>{msg.content}</p>
					</li>
				{/each}
			</ul>
		</div>
		<div>
			<button on:click|preventDefault="{scrollMessageBottom}" class="bg-secondary text-white p-1 w-full">Scroll to bottom</button>
			<form id="form-message" class="z-9 bottom-0 flex bg-primary p-4 w-full justify-end items-center" on:submit|preventDefault="{sendMsg}">
				<input class="bg-neutral w-full text-black dark:text-white outline-none focus:outline-2 focus:outline-secondary lg:w-3/5 transition-all duration-150" bind:value="{msg}" placeholder="message">
				<button class="lg:w-1/12 bg-neutral text-black hover:bg-secondary hover:text-white transition-all duration-150">Send</button>
			</form>
		</div>
	{/if}
</main>

<style lang="scss">
	#form-message * {
		@apply md:m-1 m-0.5 md:p-1 p-3 h-full rounded-lg md:text-lg text-sm;
	}

	#name-form * {
		@apply p-2 rounded-md m-1 transition-all duration-150;
	}
</style>
