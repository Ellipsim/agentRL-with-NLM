

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b7)
(on b3 b5)
(on b4 b2)
(on b5 b4)
(ontable b6)
(on b7 b8)
(on b8 b6)
(ontable b9)
(on b10 b3)
(clear b1)
(clear b10)
)
(:goal
(and
(on b4 b10)
(on b6 b3)
(on b8 b7)
(on b9 b8)
(on b10 b2))
)
)


