import { useState, useCallback, ChangeEvent } from 'react';
import { FormErrors } from '../types';

interface UseFormOptions<T> {
  initialValues: T;
  validate?: (values: T) => FormErrors;
  onSubmit?: (values: T) => void | Promise<void>;
}

export const useForm = <T extends Record<string, any>>(
  options: UseFormOptions<T>
) => {
  const [values, setValues] = useState<T>(options.initialValues);
  const [errors, setErrors] = useState<FormErrors>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = useCallback(
    (event: ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
      const { name, value, type } = event.target;
      
      setValues(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? (event.target as HTMLInputElement).checked : value,
      }));

      // Clear error when user starts typing
      if (errors[name]) {
        setErrors(prev => {
          const newErrors = { ...prev };
          delete newErrors[name];
          return newErrors;
        });
      }
    },
    [errors]
  );

  const handleBlur = useCallback(
    (event: ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
      const { name } = event.target;
      setTouched(prev => ({ ...prev, [name]: true }));

      // Validate field on blur if validator is provided
      if (options.validate) {
        const fieldErrors = options.validate(values);
        if (fieldErrors[name]) {
          setErrors(prev => ({ ...prev, [name]: fieldErrors[name] }));
        }
      }
    },
    [values, options.validate]
  );

  const setValue = useCallback((name: keyof T, value: any) => {
    setValues(prev => ({ ...prev, [name]: value }));
  }, []);

  const setFieldError = useCallback((name: string, error: string) => {
    setErrors(prev => ({ ...prev, [name]: error }));
  }, []);

  const clearErrors = useCallback(() => {
    setErrors({});
  }, []);

  const reset = useCallback(() => {
    setValues(options.initialValues);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);
  }, [options.initialValues]);

  const validate = useCallback(() => {
    if (!options.validate) return true;
    
    const validationErrors = options.validate(values);
    setErrors(validationErrors);
    
    return Object.keys(validationErrors).length === 0;
  }, [values, options.validate]);

  const handleSubmit = useCallback(
    async (event?: React.FormEvent) => {
      if (event) {
        event.preventDefault();
      }

      setIsSubmitting(true);
      
      try {
        // Validate form
        const isValid = validate();
        if (!isValid) {
          return;
        }

        // Call onSubmit if provided
        if (options.onSubmit) {
          await options.onSubmit(values);
        }
      } catch (error) {
        console.error('Form submission error:', error);
      } finally {
        setIsSubmitting(false);
      }
    },
    [values, validate, options.onSubmit]
  );

  const getFieldProps = useCallback(
    (name: keyof T) => ({
      name: name as string,
      value: values[name] || '',
      onChange: handleChange,
      onBlur: handleBlur,
    }),
    [values, handleChange, handleBlur]
  );

  const getFieldError = useCallback(
    (name: keyof T) => {
      return touched[name as string] ? errors[name as string] : undefined;
    },
    [touched, errors]
  );

  return {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    setValue,
    setFieldError,
    clearErrors,
    reset,
    validate,
    handleSubmit,
    getFieldProps,
    getFieldError,
  };
};

export default useForm;