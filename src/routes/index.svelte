<script>
	import { io } from "socket.io-client";

	let authenticated = false;
	let name = "rere";
	let messages = [];
	let msg = "";
	let sendMsg;

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
	function button() {
		msg = window.location.origin
	}

</script>

<main>
	{#if !authenticated}
		<form on:submit|preventDefault="{submit}">
			<input bind:value="{name}" placeholder="name">
			<button>Submit</button>
		</form>
	{:else}
		<form on:submit|preventDefault="{sendMsg}">
			<input bind:value="{msg}" placeholder="message">
			<button>Send</button>
		</form>
	{/if}
	<ul>
		{#each messages as msg}
			<li style="{msg.sender === 'System' ? 'color: #3182ce' : ''}">{@html msg.sender}: {@html msg.content}</li>
		{/each}
	</ul>
</main>

