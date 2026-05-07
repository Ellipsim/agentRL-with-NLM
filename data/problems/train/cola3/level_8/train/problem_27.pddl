

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(on b3 b6)
(on b4 b9)
(on b5 b3)
(on b6 b4)
(ontable b7)
(on b8 b2)
(on b9 b8)
(on b10 b5)
(clear b7)
(clear b10)
)
(:goal
(and
(on b1 b2)
(on b2 b7)
(on b7 b9)
(on b8 b5)
(on b10 b8))
)
)


