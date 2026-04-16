(set-logic ALL)
; Constraint ID: abdc6810ee3bf8eb
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59260)) (False)
(assert (not (= x 59260)))

; Query: ((== x 59261)) (False)
(assert (not (not (= x 59261))))

(check-sat)
(get-model)
