

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on-table b1)
(on b2 b10)
(on b3 b7)
(on b4 b2)
(on b5 b8)
(on b6 b9)
(on b7 b5)
(on-table b8)
(on b9 b4)
(on b10 b3)
(clear b1)
(clear b6)
)
(:goal
(and
(on b2 b9)
(on b3 b10)
(on b4 b8)
(on b5 b6)
(on b6 b3)
(on b8 b2)
(on b9 b7))
)
)


