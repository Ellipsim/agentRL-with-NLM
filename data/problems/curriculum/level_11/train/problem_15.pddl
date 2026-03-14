

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on b1 b9)
(on b2 b6)
(on-table b3)
(on-table b4)
(on b5 b11)
(on b6 b7)
(on-table b7)
(on b8 b1)
(on b9 b13)
(on b10 b5)
(on b11 b4)
(on b12 b3)
(on b13 b10)
(clear b2)
(clear b8)
(clear b12)
)
(:goal
(and
(on b4 b9)
(on b5 b2)
(on b6 b3)
(on b7 b4)
(on b8 b7)
(on b9 b11)
(on b10 b12)
(on b11 b1)
(on b12 b6))
)
)


