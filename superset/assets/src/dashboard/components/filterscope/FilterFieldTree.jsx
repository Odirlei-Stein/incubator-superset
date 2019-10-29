/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
import React from 'react';
import PropTypes from 'prop-types';
import CheckboxTree from 'react-checkbox-tree';

import 'react-checkbox-tree/lib/react-checkbox-tree.css';
import {
  CheckboxChecked,
  CheckboxUnchecked,
  CheckboxHalfChecked,
} from '../../../components/CheckboxIcons';
import renderFilterFieldTreeNodes from './renderFilterFieldTreeNodes';
import { filterScopeSelectorTreeNodePropShape } from '../../util/propShapes';

const propTypes = {
  activeKey: PropTypes.string.isRequired,
  nodes: PropTypes.arrayOf(filterScopeSelectorTreeNodePropShape).isRequired,
  checked: PropTypes.arrayOf(
    PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  ).isRequired,
  expanded: PropTypes.arrayOf(
    PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  ).isRequired,
  onCheck: PropTypes.func.isRequired,
  onExpand: PropTypes.func.isRequired,
  onClick: PropTypes.func.isRequired,
};

const FILTER_FIELD_CHECKBOX_TREE_ICONS = {
  check: <CheckboxChecked />,
  uncheck: <CheckboxUnchecked />,
  halfCheck: <CheckboxHalfChecked />,
  expandClose: <span className="rct-icon rct-icon-expand-close" />,
  expandOpen: <span className="rct-icon rct-icon-expand-open" />,
  expandAll: <span className="rct-icon rct-icon-expand-all" />,
  collapseAll: <span className="rct-icon rct-icon-collapse-all" />,
  parentClose: <span className="rct-icon rct-icon-parent-close" />,
  parentOpen: <span className="rct-icon rct-icon-parent-open" />,
  leaf: <span className="rct-icon rct-icon-leaf" />,
};

export default function FilterFieldTree({
  activeKey = '',
  nodes = [],
  checked = [],
  expanded = [],
  onClick,
  onCheck,
  onExpand,
}) {
  return (
    <CheckboxTree
      showExpandAll
      showNodeIcon={false}
      expandOnClick
      nodes={renderFilterFieldTreeNodes({ nodes, activeKey })}
      checked={checked}
      expanded={expanded}
      onClick={onClick}
      onCheck={onCheck}
      onExpand={onExpand}
      icons={FILTER_FIELD_CHECKBOX_TREE_ICONS}
    />
  );
}

FilterFieldTree.propTypes = propTypes;