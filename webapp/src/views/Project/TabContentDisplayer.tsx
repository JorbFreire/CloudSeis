import { useCommandsStore } from 'store/commandsStore'

import CommandParameters from 'components/CommandParameters';
import InputSelectorOptions from 'components/InputSelectorOptions';
import { StaticTabKey } from 'enums/StaticTabKey'

export default function TabContentDisplayer() {
  const {
    commands,
    selectedCommandIndex,
  } = useCommandsStore((state) => ({
    commands: state.commands,
    selectedCommandIndex: state.selectedCommandIndex,
  }))

  const getTabContent = () => {
    switch (selectedCommandIndex) {
      case StaticTabKey.Input:
        return <InputSelectorOptions />

      case StaticTabKey.Output:
        return <h1> OUT PUT TAB </h1>

      default:
        return (
          <CommandParameters
            command={commands.find(({ id }) => id == selectedCommandIndex)}
          />
        )
    }
  }

  return selectedCommandIndex && getTabContent()
}