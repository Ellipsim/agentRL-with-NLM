

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b2)
(on b2 b9)
(on b3 b5)
(on-table b4)
(on b5 b8)
(on-table b6)
(on b7 b4)
(on b8 b7)
(on b9 b10)
(on b10 b3)
(clear b1)
(clear b6)
)
(:goal
(and
(on b1 b5)
(on b2 b4)
(on b3 b6)
(on b5 b7)
(on b6 b1)
(on b7 b10)
(on b9 b3)
(on b10 b2))
)
)


