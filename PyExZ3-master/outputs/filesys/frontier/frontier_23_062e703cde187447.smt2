(set-logic ALL)
; Constraint ID: 062e703cde187447
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60244)) (False)
(assert (not (= x 60244)))

; Query: ((== x 60245)) (False)
(assert (not (not (= x 60245))))

(check-sat)
(get-model)
