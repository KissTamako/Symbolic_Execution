(set-logic ALL)
; Constraint ID: 1c2a34bddd4b110c
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60211)) (False)
(assert (not (= x 60211)))

; Query: ((== x 60212)) (False)
(assert (not (not (= x 60212))))

(check-sat)
(get-model)
