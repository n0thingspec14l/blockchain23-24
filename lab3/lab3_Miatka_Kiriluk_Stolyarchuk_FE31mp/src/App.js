import {useEffect, useState} from "react";
import {ethers} from "ethers";
import Modal from "./Modal";

function App() {
    const [connected, setConnected] = useState(false);
    const [walletAddress, setWalletAddress] = useState("");
    const [balance, setBalance] = useState('')
    const [provider, setProvider] = useState()
    const [inputText, setInputText] = useState('')
    const [signedMassages, setSignedMassages] = useState([
        {
            text: 'This is first test message for 3-rd lab',
            address: '0x2562Bd1b5dDdd9D4CF1c0E5b616D742aCfF79F32',
            signature: '0x0bd9154a725ee05f0fa130e58f2bc83fa549605606961c95c580aebee375fd372deba94f16e1b000d01476560108ea178027eceba0ea59fb308a4ac47679d9c81b'
        },
        {
            text: 'This is second test message for 3-rd lab',
            address: '0x2562Bd1b5dDdd9D4CF1c0E5b616D742aCfF79F32',
            signature: '0x21f44c3574b81309b4e8875e79a88a269d5e00b2766de65c1e0f832d5ce46b1836df101098785737450852f57340780892309400a5c57c71c999877b906fba801c'
        }
    ])
    const [signer, setSigner] = useState()

    async function connectWallet() {
        try {
            const signer = await provider.getSigner();
            setSigner(signer)
            const walletAddress = await signer.getAddress();
            await provider.getBalance(walletAddress).then(res => setBalance(ethers.formatEther(res)))
            setConnected(true);
            setWalletAddress(walletAddress);
        } catch (e) {
            alert('Something went wrong. Follow the instruction below to sign in\n 1 - Install MetaMask \n 2 - Connect wallet using button below')
        }
    }

    const handleSubmit =  async (e) => {
        e.preventDefault()
        if (inputText.length === 0) {
            alert('You can\'t sign an empty massage')
        } else {
            const signature = await signer.signMessage(inputText)
            setSignedMassages(prevState => [...prevState, {
                text: inputText,
                address: walletAddress,
                signature
            }])
        }
    }

    const handleCopy = (text) => {
        navigator.clipboard.writeText(text)
        alert('Copied to clipboard!')
    }

    useEffect(() => {
        if (window.ethereum == null) {
            alert("MetaMask not installed; using read-only defaults")
            setProvider(ethers.getDefaultProvider())
        } else {
            setProvider(new ethers.BrowserProvider(window.ethereum))
        }
    }, [])

    return (
        <>
            {!connected ? <Modal connectWallet={connectWallet}/> :
                <div className="main">
                    <div className="content-info__wrapper">
                        <div className="content__info">
                            <h1>Wallet address:</h1>
                            <p>{walletAddress}</p>
                            <h1>Balance:</h1>
                            <p>{balance} ETH</p>
                        </div>
                        <div className="content__info-footer">
                            <h2>Tips:</h2>
                            <p>1) Click on <strong>"signed message"</strong> or <strong>"signed by"</strong> value to copy it</p>
                            <p>2) Use <a href="https://etherscan.io/verifiedSignatures" target={"_blank"}>*CLICK*</a> link to verify the sign</p>
                        </div>
                    </div>
                        <div className="content-form__wrapper">
                            <div className="content__form">
                                <h1>Sign your massage:</h1>
                                <form className='content__form-self'>
                                    <input className='content__form-input' type="text" placeholder='Write your massage' onChange={e => setInputText(e.target.value)}/>
                                    <button onClick={handleSubmit} className='content__form-btn'>Sign</button>
                                </form>
                                <div className='content__signed'>
                                    {signedMassages.map((el,i) =>
                                        <div className='signed__massages' key={i}>
                                            <p>Signed message: <span onClick={() => handleCopy(el.text)}>{el.text}</span></p>
                                            <p>Signed by: <span onClick={() => handleCopy(el.address)}>{el.address}</span></p>
                                            <p>Signature for check: <button className='content_sign-btn' onClick={() => handleCopy(el.signature)}>
                                                Click to copy
                                            </button>
                                            </p>
                                        </div>
                                    )}
                                </div>
                            </div>
                    </div>
                </div>
                }
        </>
    );
}

export default App;