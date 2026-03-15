

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on-table b1)
(on b2 b5)
(on b3 b9)
(on b4 b1)
(on-table b5)
(on b6 b7)
(on b7 b8)
(on b8 b4)
(on b9 b2)
(on b10 b6)
(clear b3)
(clear b10)
)
(:goal
(and
(on b1 b4)
(on b2 b1)
(on b3 b8)
(on b4 b5)
(on b6 b9)
(on b8 b7)
(on b10 b2))
)
)


