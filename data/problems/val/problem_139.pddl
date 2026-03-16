

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b4)
(on b3 b8)
(on b4 b1)
(on b5 b10)
(ontable b6)
(on b7 b2)
(on b8 b9)
(ontable b9)
(on b10 b11)
(ontable b11)
(on b12 b3)
(clear b5)
(clear b7)
(clear b12)
)
(:goal
(and
(on b1 b4)
(on b3 b7)
(on b4 b9)
(on b5 b11)
(on b6 b8)
(on b7 b5)
(on b8 b12)
(on b10 b6)
(on b12 b2))
)
)


