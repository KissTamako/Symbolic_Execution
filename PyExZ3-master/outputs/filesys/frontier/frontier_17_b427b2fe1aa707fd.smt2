(set-logic ALL)
; Constraint ID: b427b2fe1aa707fd
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59560)) (False)
(assert (not (= x 59560)))

; Query: ((== x 59561)) (False)
(assert (not (not (= x 59561))))

(check-sat)
(get-model)
