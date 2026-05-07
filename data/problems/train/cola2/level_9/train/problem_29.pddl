

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b11)
(on b3 b5)
(ontable b4)
(ontable b5)
(ontable b6)
(on b7 b3)
(ontable b8)
(on b9 b8)
(on b10 b9)
(on b11 b1)
(clear b2)
(clear b4)
(clear b7)
(clear b10)
)
(:goal
(and
(on b1 b11)
(on b2 b10)
(on b3 b6)
(on b4 b7)
(on b6 b1)
(on b8 b5)
(on b9 b2)
(on b11 b9))
)
)


