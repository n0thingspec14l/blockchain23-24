import React from 'react';

const Modal = (props) => {
    return (
        <div className="modal__wrapper">
            <div className="modal__content">
                <h1 className='modal__header'>Connect to MetaMask wallet</h1>
                <button className="modal__connect" onClick={props.connectWallet}>Connect</button>
            </div>
        </div>
    );
};

export default Modal;