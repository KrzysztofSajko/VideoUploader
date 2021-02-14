from dataclasses import dataclass
from typing import Optional

from .filename_schema import FileNameSchema


@dataclass
class FileNameProcessor:
    schema: FileNameSchema

    def get_title(self, filename: str) -> str:
        title = ""
        for old, new in self.schema.change.items():
            filename = filename.replace(old, new)

        split = filename.split(self.schema.separator)

        for i, item_descriptor in enumerate(self.schema.items):
            if i >= len(split):
                if item_descriptor.required:
                    raise KeyError(f'Filename missing required item "{item_descriptor.name}"')
                else:
                    continue

            title = f'{title} {item_descriptor.prefix}{split[i]}{item_descriptor.suffix}'

        return title

    def get_item(self, filename: str, item_name: str) -> Optional[str]:
        position = self.schema.get_item_position(item_name)
        if position is not None:
            return filename.split(self.schema.separator)[position]
