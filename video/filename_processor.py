from dataclasses import dataclass
from .filename_schema import FileNameSchema


@dataclass
class FileNameProcessor:
    schema: FileNameSchema

    def get_title(self, filename: str) -> str:
        title = ""
        for key, value in self.schema.change.items():
            filename = filename.replace(key, value)

        split = filename.split(self.schema.separator)

        for i, item_descriptor in enumerate(self.schema.items):
            if i >= len(split):
                if item_descriptor.required:
                    raise KeyError(f'Filename missing required field "{item_descriptor.name}"')
                else:
                    continue

            title = f'{title} {item_descriptor.prefix}{split[i]}{item_descriptor.suffix}'

        return title
