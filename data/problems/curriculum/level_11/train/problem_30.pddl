

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b9)
(on b2 b6)
(on b3 b1)
(on-table b4)
(on b5 b8)
(on b6 b7)
(on b7 b3)
(on b8 b2)
(on b9 b11)
(on b10 b4)
(on b11 b12)
(on b12 b10)
(clear b5)
)
(:goal
(and
(on b1 b3)
(on b2 b4)
(on b5 b2)
(on b6 b10)
(on b8 b6)
(on b9 b8)
(on b11 b1)
(on b12 b7))
)
)


