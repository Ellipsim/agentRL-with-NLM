

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b3)
(on b2 b4)
(on b3 b5)
(on b4 b11)
(on b5 b8)
(on b6 b12)
(on b7 b9)
(on b8 b2)
(on b9 b1)
(on-table b10)
(on-table b11)
(on b12 b10)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b8)
(on b2 b5)
(on b4 b1)
(on b5 b9)
(on b8 b12)
(on b9 b10)
(on b11 b4)
(on b12 b7))
)
)


