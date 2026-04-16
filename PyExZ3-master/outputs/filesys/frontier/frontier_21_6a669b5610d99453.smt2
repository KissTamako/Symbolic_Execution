(set-logic ALL)
; Constraint ID: 6a669b5610d99453
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59341)) (False)
(assert (not (= x 59341)))

; Query: ((== x 59342)) (False)
(assert (not (not (= x 59342))))

(check-sat)
(get-model)
