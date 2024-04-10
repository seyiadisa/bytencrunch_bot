import { Select, SelectItem } from "@nextui-org/react";

// import WebApp from '@twa-dev/sdk'

export default function HomePage() {
	return (
		<>

			<h1>Pick a vendor</h1>
			<Select label="Choose a vendor" className="max-w-xs">
				<SelectItem key="1" value="hello">hello</SelectItem>
			</Select>
		</>
	)
}