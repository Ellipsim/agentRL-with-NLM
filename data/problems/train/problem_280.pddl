

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b8)
(on b3 b4)
(on b4 b7)
(ontable b5)
(on b6 b10)
(ontable b7)
(on b8 b6)
(ontable b9)
(on b10 b9)
(clear b1)
(clear b2)
(clear b5)
)
(:goal
(and
(on b3 b2)
(on b4 b3)
(on b7 b1)
(on b8 b5)
(on b9 b7)
(on b10 b8))
)
)


