import React from 'react';
import { Classes } from '@blueprintjs/core';

import '@blueprintjs/core/lib/css/blueprint.css';

import QKTMainPage from 'components/QKTMainPage';

import 'styles/App.css';


const App = () => (
  <div
    className={`App`}
    style={{ width: '100%', height: '100%' }}
  >
    <QKTMainPage />
  </div>
);

export default App;
